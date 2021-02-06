#pragma once
#include <openssl/md5.h>
#include <sys/stat.h>
#include <fstream>
#include <sstream>
#include <cstdio>
#include <iterator>
#include <iomanip>
using namespace std;

const string WHITELIST_PATH = "whitelist.fp";
const string BLACKLIST_PATH = "blacklist.hdb";

bool isfile(const char *path)
{
    struct stat fileStat;
    return !(stat(path, &fileStat) || !S_ISREG(fileStat.st_mode));
}

class db_contents
{
private:
    ifstream source;

public:
    db_contents(const string &path)
    {
        source.open(path);
    }
    istream_iterator<string> begin()
    {
        return {source};
    }
    istream_iterator<string> end()
    {
        return {};
    }
};

class DataBase
{
private:
    const static size_t BUF_SIZE = 65536;
    // efficiently calculates file hash
    static string hash(const string &path)
    {
        unsigned char hash[MD5_DIGEST_LENGTH];
        unsigned char data[BUF_SIZE];
        FILE *File = fopen(path.c_str(), "rb");
        stringstream result;
        MD5_CTX md5;
        MD5_Init(&md5);
        size_t bytes;
        while ((bytes = fread(data, 1, BUF_SIZE, File)) != 0)
            MD5_Update(&md5, data, bytes);
        fclose(File);
        MD5_Final(hash, &md5);
        for (size_t i = 0; i < MD5_DIGEST_LENGTH; i++)
            result << hex << setw(2) << setfill('0') << (int)hash[i];
        return result.str();
    }
    // generates valid libclamav signature
    static string signature(const string &path)
    {
        if (isfile(path.c_str()))
        {
        struct stat stat_buf;
        stat(path.c_str(), &stat_buf);
        stringstream sig;
        sig << hash(path) << ':' << stat_buf.st_size << ':' << "CustomSignature" << endl;
        return sig.str();
        }
        else
            throw invalid_argument("file does not exist");
    }
    // removes signature from database
    static void remove_signature(const string &sig, const string &db)
    {
        ifstream r(db);
        ofstream w(db + "_temp");
        string t;
        getline(r, t);
        while (r)
        {
            t += "\n";
            if (t != sig)
                w << t;
            getline(r, t);
        }
        r.close();
        w.close();
        remove(db.c_str());
        rename((db + "_temp").c_str(), db.c_str());
    }

public:
    // adds file signature to whitelist
    static void whitelist(const string &path)
    {
        string sig;
        if (isfile(path.c_str()))
            sig = signature(path);
        else
            throw invalid_argument("file does not exist");
        ofstream f(WHITELIST_PATH, ios::app);
        f << sig;
        f.close();
        remove_signature(sig, BLACKLIST_PATH);
    }
    // adds file signature to blacklist
    static void blacklist(const string &path)
    {
        string sig;
        if (isfile(path.c_str()))
            sig = signature(path);
        else
            throw invalid_argument("file does not exist");
        ofstream f(BLACKLIST_PATH, ios::app);
        f << sig;
        f.close();
        remove_signature(sig, WHITELIST_PATH);
    }
    // returns contents of the database
    static db_contents get_db_iterator(const string &path)
    {
        if (isfile(path.c_str()))
            return db_contents(path);
        else
            throw invalid_argument("file does not exist");
    }
    // returns file signature if the database contains it
    static string find(const string &path, const string &db)
    {
        string sig;
        if (isfile(path.c_str()))
        {
            sig = signature(path);
            sig = sig.substr(0, sig.length() - 1);
        }
        else
            throw invalid_argument("file does not exist");
        for (const string &i : get_db_iterator(db))
            if (i == sig)
                return sig;
        return "";
    }
};

void enqueue_scan(const string &path, const string &fifo_path = "/tmp/cobra.sock")
{
    if (isfile(path.c_str()))
    {
        ofstream pipe(fifo_path);
        pipe << path;
        pipe.close();
    }
    else
        throw invalid_argument("file does not exist");
}
