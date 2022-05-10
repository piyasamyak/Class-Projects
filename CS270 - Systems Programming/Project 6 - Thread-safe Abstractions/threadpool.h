#ifndef THREADPOOL_H
#define THREADPOOL_H
#define MAXTHREADS 12 // arbitrary limit

#include "pq.h"

typedef struct threadpool_t
{ /* YOUR CODE HERE */
    pq_t *queue;
    pthread_t *pool;
} threadpool_t;

typedef struct task_t
{
    void (*task)(void *);
    void *arg;
} task_t;

/* Create and return a pointer to an instance of the type
 * declared above.
 */
threadpool_t *tp_create(int nthreads);

/* Submit a job (task) to be executed by the given thread pool.
 * Jobs are functions that will be executed in a pool thread,
 * and passed the given parameter (arg).  Jobs are executed
 * in priority order, with higher priorities executed first.
 * Starvation of a low-priority job is possible if jobs with
 * higher priorities are submitted continually.
 */
void tp_submit(threadpool_t *tp, void (*job)(void *),
               void *arg, short prio);
#endif