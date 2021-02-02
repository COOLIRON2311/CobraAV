#pragma once
#include <unordered_set>
using namespace std;

size_t CACHE_MAX_SIZE = 100;

class Cache
{
private:
    unordered_set<size_t> data;
    inline void update()
    {
        if (data.size() >= CACHE_MAX_SIZE)
            data.clear();
    }

public:
    Cache()
    {
        data.reserve(CACHE_MAX_SIZE);
    }
    ~Cache()
    {
        data.clear();
    }
    bool contains(size_t item) const
    {
        return data.find(item) != data.end();
    }
    void add(size_t item)
    {
        update();
        data.insert(item);
    }
};
