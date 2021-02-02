#pragma once
#include <sys/stat.h>
#include <string>
using namespace std;

class File
{
    int st_code;

public:
    string path;
    bool cache;
    size_t Hash;
    struct stat Stat;
    File(const string &path, bool cache=false) : path(path), cache(cache)
    {
        st_code = stat(path.c_str(), &Stat);
        Hash = hash<string>()(path + to_string(Stat.st_ctime));
    }
    string Name() const
    {
        return path.substr(path.rfind('/') + 1);
    }
    operator bool() const
    {
        return !st_code && S_ISREG(Stat.st_mode);
    }
};
