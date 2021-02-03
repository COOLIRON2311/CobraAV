#include "av_engine.h"
#include "cobra-sentnel.h"

int main(int argc, char **argv)
{
    setvbuf(stdout, NULL, _IONBF, BUFSIZ);
    if (argc < 2)
    {
        printf("Usage: %s directories\n", argv[0]);
        return 2;
    }

    if (setup() == 2)
        return 2;

    // Create the file system watcher instance
    // FileWatcher allow a first boolean parameter that indicates if it should start with the generic file watcher instead of the platform specific backend
    FileWatcher *fileWatcher = new FileWatcher();

    // Create the instance of your FileWatcherListener implementation
    UpdateListener *listener = new UpdateListener();

    // Add a folder to watch, and get the WatchID
    // It will watch the /tmp folder recursively ( the third parameter indicates that is recursive )
    // Reporting the files and directories changes to the instance of the listener
    for (size_t i = 1; i < argc; i++)
        fileWatcher->addWatch(argv[i], listener, true);

    fileWatcher->watch();

    while (true)
    {
        listener->process_queue();
        usleep(1);
    }
}
