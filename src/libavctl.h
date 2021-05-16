#pragma once
#include <openssl/md5.h>
#include <sys/stat.h>
#include <fstream>
#include <sstream>
#include <cstdio>
#include <iterator>
#include <iomanip>

const std::string WHITELIST_PATH = "whitelist.fp";
const std::string BLACKLIST_PATH = "blacklist.hdb";

bool isfile(const char *path)
{
    struct stat fileStat;
    return !(stat(path, &fileStat) || !S_ISREG(fileStat.st_mode));
}

class db_contents
{
private:
    std::ifstream source;

public:
    db_contents(const std::string &path)
    {
        source.open(path);
    }
    std::istream_iterator<std::string> begin()
    {
        return {source};
    }
    std::istream_iterator<std::string> end()
    {
        return {};
    }
};

class DataBase
{
private:
    const static size_t BUF_SIZE = 65536;
    // efficiently calculates file hash
    static std::string hash(const std::string &path)
    {
        unsigned char hash[MD5_DIGEST_LENGTH];
        unsigned char data[BUF_SIZE];
        FILE *File = fopen(path.c_str(), "rb");
        std::stringstream result;
        MD5_CTX md5;
        MD5_Init(&md5);
        size_t bytes;
        while ((bytes = fread(data, 1, BUF_SIZE, File)) != 0)
            MD5_Update(&md5, data, bytes);
        fclose(File);
        MD5_Final(hash, &md5);
        for (size_t i = 0; i < MD5_DIGEST_LENGTH; i++)
            result << std::hex << std::setw(2) << std::setfill('0') << (int)hash[i];
        return result.str();
    }
    // generates valid libclamav signature
    static std::string signature(const std::string &path)
    {
        if (isfile(path.c_str()))
        {
            struct stat stat_buf;
            stat(path.c_str(), &stat_buf);
            std::stringstream sig;
            sig << hash(path) << ':' << stat_buf.st_size << ':' << "CustomSignature" << std::endl;
            return sig.str();
        }
        else
            throw std::invalid_argument("file does not exist");
    }
    // removes signature from database
    static void remove_signature(const std::string &sig, const std::string &db)
    {
        std::ifstream r(db);
        std::ofstream w(db + "_temp");
        std::string t;
        struct stat st;
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
        stat((db + "_temp").c_str(), &st);
        if (st.st_size == 0)
            remove((db + "_temp").c_str());
        else
            rename((db + "_temp").c_str(), db.c_str());
    }

public:
    // adds file signature to whitelist
    static void whitelist(const std::string &path)
    {
        std::string sig;
        if (isfile(path.c_str()))
            sig = signature(path);
        else
            throw std::invalid_argument("file does not exist");
        std::ofstream f(WHITELIST_PATH, std::ios::app);
        f << sig;
        f.close();
        remove_signature(sig, BLACKLIST_PATH);
    }
    // adds file signature to blacklist
    static void blacklist(const std::string &path)
    {
        std::string sig;
        if (isfile(path.c_str()))
            sig = signature(path);
        else
            throw std::invalid_argument("file does not exist");
        std::ofstream f(BLACKLIST_PATH, std::ios::app);
        f << sig;
        f.close();
        remove_signature(sig, WHITELIST_PATH);
    }
    // returns contents of the database
    static db_contents get_db_iterator(const std::string &path)
    {
        if (isfile(path.c_str()))
            return db_contents(path);
        else
            throw std::invalid_argument("file does not exist");
    }
    // returns file signature if the database contains it
    static std::string find(const std::string &path, const std::string &db)
    {
        std::string sig;
        if (isfile(path.c_str()))
        {
            sig = signature(path);
            sig = sig.substr(0, sig.length() - 1);
        }
        else
            throw std::invalid_argument("file does not exist");
        for (const std::string &i : get_db_iterator(db))
            if (i == sig)
                return sig;
        return "";
    }
};

void enqueue_scan(const std::initializer_list<std::string> &files, const std::string &fifo_path = "/tmp/cobra.sock")
{
    for (const std::string &path : files)
        if (isfile(path.c_str()))
        {
            std::ofstream pipe(fifo_path);
            pipe << path + '\n';
            pipe.close();
        }
        else
            throw std::invalid_argument("file does not exist");
}

void send_reload()
{
    system("systemctl restart cobra-sentinel.service");
}
