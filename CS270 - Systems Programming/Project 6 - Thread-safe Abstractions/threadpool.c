#include "threadpool.h"

void *thread_job(void *arg)
{
    pq_t *tpQueue = (pq_t *)arg;
    while (1)
    {
        // get the next task in the queue
        task_t *task = (task_t *)pq_next(tpQueue);

        // execute the task
        task->task(task->arg);
    }
}

/* Create and return a pointer to an instance of the type
 * declared above. */
threadpool_t *tp_create(int nthreads)
{
    // Create thread_pool
    struct threadpool_t *thread_pool = (threadpool_t *)malloc(sizeof(threadpool_t));
    thread_pool->pool = (pthread_t *)malloc(sizeof(pthread_t[nthreads]));

    // Create a priority queue for the thread_pool
    thread_pool->queue = pq_create();

    // Create pool of threads
    for (int i = 0; i < nthreads; i++)
    {
        if (pthread_create(&thread_pool->pool[i], NULL, thread_job, &thread_pool->queue) != 0)
        {
            perror("Failed to create thread.\n");
            exit(0);
        }
    }
    return thread_pool;
}

/* Submit a job (task) to be executed by the given thread pool.
 * Jobs are functions that will be executed in a pool thread,
 * and passed the given parameter (arg).  Jobs are executed
 * in priority order, with higher priorities executed first.
 * Starvation of a low-priority job is possible if jobs with
 * higher priorities are submitted continually.
 */
void tp_submit(threadpool_t *tp, void (*job)(void *), void *arg, short prio)
{
    // create a task
    struct task_t *new_task = (task_t *)malloc(sizeof(task_t));
    new_task->task = job;
    new_task->arg = arg;

    // place task_t in the queue
    pq_insert(tp->queue, new_task, prio);
}