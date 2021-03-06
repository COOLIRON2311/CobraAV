#include <unistd.h>
#include <poll.h>
#include <sys/ioctl.h>
#include "av_engine.h"
#include "cobra-sentinel.h"

const char *FIFO_PATH = "/tmp/cobra.sock";

int main(int argc, char **argv)
{
    setvbuf(stdout, NULL, _IONBF, BUFSIZ);
    if (argc < 10)
    {
        printf("Usage:\ncobra-sentinel -msize <bytes> -threat <0/1> -t <dirs> -e <wildcards> -q <path>\n");
        return 2;
    }

    if (setup() == 2)
        return 2;

    // Create the file system watcher instance
    // FileWatcher allow a first boolean parameter that indicates if it should start with the generic file watcher instead of the platform specific backend
    FileWatcher *fileWatcher = new FileWatcher();

    // Create the instance of your FileWatcherListener implementation
    UpdateListener *listener = new UpdateListener();

    // Parse trivial config parameters
    listener->maxfsize = atoi(argv[2]);
    listener->remove_threat = atoi(argv[4]);
    listener->quarantine_path = argv[argc-1];
    size_t i = 6;
    while (strcmp(argv[i], "-e") != 0)
        // Add a folder to watch, and get the WatchID
        // It will watch the /tmp folder recursively ( the third parameter indicates that is recursive )
        // Reporting the files and directories changes to the instance of the listener
        fileWatcher->addWatch(argv[i++], listener, true);
    i++;
    while (strcmp(argv[i], "-q") != 0)
    {
        // Add wildcards to scan exceptions list
        try
        {
            listener->exceptions.emplace_back(argv[i++], regex_constants::extended);
        }
        catch (regex_error& e)
        {
            cout << e.what() << ": ignored " << argv[i-1] << endl;
        }
    }

    umask(0);
    string data;
    char _byte[1];
    ssize_t bytes;
    mkfifo(FIFO_PATH, 06667);
    int pipe = open(FIFO_PATH, O_RDWR|O_NONBLOCK);

    fileWatcher->watch();

    while (true)
    {
        listener->process_queue();
        while ((bytes = read(pipe, _byte, 1)) > 0)
        {
            if (*_byte == '\n')
            {
                listener->enqueue(data);
                data = "";
            }
            else
                data += *_byte;
        }
        usleep(1);
    }
}
