#pragma once
#include <unistd.h>
#include <sys/stat.h>
#include <dirent.h>
#include <iostream>
#include <fstream>
#include <queue>
#include <regex>
#include "efsw/efsw.h"
#include "efsw/efsw.hpp"
#include "av_engine.h"
#include "Cache.h"
#include "File.h"

using namespace std;
using namespace efsw;

/*
long double mb;
void update_size()
{
    mb = size * (CL_COUNT_PRECISION / 1024) / 1024.0;
}
*/

// Inherits from the abstract listener class, and implements the the file action handler
class UpdateListener : public FileWatchListener
{
private:
    queue<File> que;
    size_t infected = 0;
    Cache cache;

    static void dbg_log(const string &s)
    {
        ofstream of("dump.txt", ios::app);
        of << s << "\n";
        of.close();
    }

    string get_new_name(const File &file)
    {
        size_t ret = 0;
        struct dirent *dir;
        DIR *d = opendir(quarantine_path.c_str());
        string exclude = ".avmeta";
        if (d)
            while ((dir = readdir(d)) != NULL)
            {
                //cout << dir->d_name << endl;
                if (strstr(dir->d_name, exclude.c_str()) == NULL &&
                    strstr(dir->d_name, file.Name().c_str()) != NULL)
                    ret++;
            }
        closedir(d);
        return ret ? '.' + to_string(ret) : "";
    }

    void contain(const File &file)
    {
        string out = this->quarantine_path + '/' + file.Name() + get_new_name(file);
        rename(file.path.c_str(), out.c_str());
        ofstream meta(out + ".avmeta");
        meta << file.path << endl;
        meta << file.Stat.st_mode << endl;
        meta.close();
        chmod(out.c_str(), 0);
    }

    bool exceeds_max_size(const File &file)
    {
        return this->maxfsize != 0 && file.Stat.st_size > this->maxfsize;
    }

    bool is_exception(const File &file)
    {
        for (const auto &i : this->exceptions)
        {
            if (regex_match(file.path, i))
            {
                // cout << "MATCH: " << path << endl;
                return true;
            }
        }
        return false;
    }

public:
    size_t maxfsize;
    string quarantine_path;
    bool remove_threat;
    list<regex> exceptions;

    UpdateListener() {}
    inline void enqueue(const File &file)
    {
        que.push(file);
    }
    void process_queue()
    {
        while (!que.empty())
        {
            File file = que.front();
            if (!cache.contains(file.Hash))
            {
                int ret = scan(file.path.c_str());

                if (!file.cache && ret == 0) // manually enqueued file is clean
                    printf("%s: Clean\n", file.path.c_str());

                if (ret == 1) // only store infected files
                {
                    if (file.cache)
                        cache.add(file.Hash);
                    else
                    { // manually enqueued file is infected
                        if (this->remove_threat)
                            remove(file.path.c_str());
                        else
                            contain(file);
                    }
                    // dbg_log(file.path);
                    // infected++;
                    // cout << infected << endl;
                }
                // update_size();
            }
            if (cache.contains(file.Hash))
            {
                if (this->remove_threat)
                    remove(file.path.c_str());
                else
                    contain(file);
            }
            que.pop();
        }
    }

    void handleFileAction(WatchID watchid, const string &dir, const string &filename, Action action, string oldFilename = "") override
    {
        File file(dir + filename, true);
        if (action == Action::Modified)
        {
            if (file && !exceeds_max_size(file) && !is_exception(file))
                enqueue(file); // add file to scan queue
        }
    }
};
