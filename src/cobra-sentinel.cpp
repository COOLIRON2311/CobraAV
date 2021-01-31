#include "av_engine.h"

int main(int argc, char **argv)
{
    setvbuf(stdout, NULL, _IONBF, BUFSIZ);
    long double mb;
    size_t infected = 0;
    if (argc < 2)
    {
        printf("Usage: %s files\n", argv[0]);
        return 2;
    }

    if (setup() == 2)
        return 2;

    for (size_t i = 1; i < argc; i++)
        if (scan(argv[i]) == 1)
            infected++;
    /* free memory */
    cl_engine_free(engine);
    /* calculate size of scanned data */
    mb = size * (CL_COUNT_PRECISION / 1024) / 1024.0;
    printf("Data scanned: %2.2Lf MB\n", mb);
    printf("Infected files: %i\n", infected);

    return ret == CL_VIRUS ? 1 : 0;
}
