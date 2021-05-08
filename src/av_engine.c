#include "av_engine.h"

int fd, ret;
unsigned long int size = 0;
unsigned int sigs = 0;
const char *virname;
struct cl_engine *engine;
struct cl_scan_options options;
const char* db_path = "/opt/cobraav/signatures";

int setup()
{
    int ret;
    if ((ret = cl_init(CL_INIT_DEFAULT)) != CL_SUCCESS)
    {
        printf("Can't initialize libclamav: %s\n", cl_strerror(ret));
        return 2;
    }

    if (!(engine = cl_engine_new()))
    {
        printf("Can't create new engine\n");
        return 2;
    }

    /* load all available databases from default directory */
    if ((ret = cl_load(db_path, engine, &sigs, CL_DB_STDOPT)) != CL_SUCCESS)
    {
        printf("cl_load: %s\n", cl_strerror(ret));
        close(fd);
        cl_engine_free(engine);
        return 2;
    }

    printf("Loaded %u signatures.\n", sigs);

    /* build engine */
    if ((ret = cl_engine_compile(engine)) != CL_SUCCESS)
    {
        printf("Database initialization error: %s\n", cl_strerror(ret));
        cl_engine_free(engine);
        close(fd);
        return 2;
    }
}

int scan(const char *filename)
{
    if ((fd = open(filename, O_RDONLY)) == -1)
    {
        printf("Can't open files %s\n", filename);
        return 2;
    }

    /* scan file descriptor */
    memset(&options, 0, sizeof(struct cl_scan_options));
    options.parse |= ~0;                           /* enable all parsers */
    // options.general |= CL_SCAN_GENERAL_HEURISTICS; /* enable heuristic alert options */
    options.general |= CL_SCAN_GENERAL_ALLMATCHES;
    if ((ret = cl_scandesc(fd, filename, &virname, &size, engine, &options)) == CL_VIRUS)
    {
        printf("%s: %s\n", filename, virname);
        close(fd);
        return 1;
    }
    else
    {
        if (ret == CL_CLEAN)
        {
            // printf("%s: No virus detected\n", filename);
            close(fd);
            return 0;
        }
        else
        {
            printf("Error: %s\n", cl_strerror(ret));
            // cl_engine_free(engine);
            close(fd);
            return 2;
        }
    }
    close(fd);
}
