
Page 1 of 4
/* Test driver for the priority queue.
 * Create some inserting threads and some removing threads.
 * Each gets a ponter to a string literal, and inserts its characters
 * one at a time into the priority queue, with priorities set to ensure
 * the come out in the order they went in.
 */
#include "pq.h"
#include <pthread.h>
#include <stdio.h> // printf, NULL
#include <string.h>
#include <stdlib.h>
#define MAXSTR 80 // max string length
#define STARTPRIO 200
#define NPAR 5 // number of insert/remove threads (each)
    typedef struct
{
    int it_index;
    short it_prio;
    char it_c;
} item_t;
typedef struct
{
    pq_t *task_q;
    int task_indx;
} task_t;
typedef struct
{
    pthread_mutex_t rbuf_rlock; // protect critical section: incount increment
    pq_t *rbuf_outq;            // result of pq_next for one string
    int rbuf_incount;
    int rbuf_expected;
} rbuf_t;
/****** globals - counter for things to insert, target total, lock *****/
static char *instrs[NPAR] =
    {"Now is the time for all good men to come to the aid of their country.",
     "Judge not, that ye be not judged.",
     "A man with a watch always knows what time it is.",
     "Nice takes time.",
     "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"};
static pthread_mutex_t glock;    // protect updates
static pthread_cond_t countcond; // main thread waits to get all
static int items_removed = 0;
static rbuf_t acc[NPAR]; // accumulators for results
void acquire_lock(pthread_mutex_t *l)
{
    char msgbuf[MAXSTR];
    int rv;
    if ((rv = pthread_mutex_lock(l)) != 0)
    {
        strerror_r(rv, msgbuf, MAXSTR);
        fprintf(stderr, "mutex_lock returned %s.\n", msgbuf);
        fflush(stdout);
        pthread_exit(NULL);
    }
}
void release_lock(pthread_mutex_t *l)
{
    char msgbuf[MAXSTR];
    int rv;
    if ((rv = pthread_mutex_unlock(l)) != 0)
    {
        strerror_r(rv, msgbuf, MAXSTR);
        fprintf(stderr, "mutex_unlock returned %s.\n", msgbuf);
        fflush(stdout);
        pthread_exit(NULL);
    }
}
void slp(pthread_cond_t *cond, pthread_mutex_t *m)
{
    int rv;
    char msgbuf[MAXSTR];
    if ((rv = pthread_cond_wait(cond, m)) != 0)
    {
        strerror_r(rv, msgbuf, MAXSTR);
        fprintf(stderr, "cond_wait returned %s.\n", msgbuf);
        fflush(stdout);
        pthread_exit(NULL);
    }
}
void wakeup(pthread_cond_t *cond)
{
    char msgbuf[MAXSTR];
    int rv;
    if ((rv = pthread_cond_signal(cond)) != 0)
    {
        strerror_r(rv, msgbuf, MAXSTR);
        fprintf(stderr, "cond_wait returned %s.\n", msgbuf);
        fflush(stdout);
        pthread_exit(NULL);
    }
}
// inserting thread - insert characters with indices, then terminate.
void *inserter(void *arg)
{
    task_t *tp = (task_t *)arg;
    char *cp = instrs[tp->task_indx];
    short prio = STARTPRIO;
    while (*cp)
    {
        item_t *item = malloc(sizeof(item_t));
        item->it_index = tp->task_indx;
        item->it_c = *cp++;
        item->it_prio = prio;
        pq_insert(tp->task_q, item, prio);
        prio -= 1;
    }
    return NULL;
}
// removing thread - take items from queue, append to the indicated array
void *remover(void *arg)
{
    pq_t *q = (pq_t *)arg;
    for (;;)
    {
        // get a task, add the character to the output queue
        item_t *item = pq_next(q); //  blocks finally
        rbuf_t *d = &acc[item->it_index];
        char c = item->it_c;
        pq_insert(d->rbuf_outq, item, item->it_prio);
        acquire_lock(&d->rbuf_rlock);
        d->rbuf_incount += 1;
        if (d->rbuf_incount == d->rbuf_expected)
        { // this one's done (in theory)
            acquire_lock(&glock);
            items_removed += d->rbuf_incount; // add to global total
            release_lock(&glock);
            wakeup(&countcond);           // wakeup anybody sleeping on this
            release_lock(&d->rbuf_rlock); // don't return while holding lock!
            return NULL;                  // We're out
        }
        release_lock(&d->rbuf_rlock);
    }
    /* NOTREACHED */
}
int main()
{
    int i, j;
    task_t tasks[NPAR];
    pthread_t tids[NPAR * 2];
    pq_t *allq;
    int total_items; // when items_removed equals this, we are done

    // initialize the output data structures
    total_items = 0;
    for (i = 0; i < NPAR; i++)
    {
        if (pthread_mutex_init(&acc[i].rbuf_rlock, 0) != 0)
        {
            printf("mutex_init failed on iteration %d.\n", i);
            exit(1);
        }
        acc[i].rbuf_outq = pq_create();
        acc[i].rbuf_expected = strlen(instrs[i]);
        total_items += acc[i].rbuf_expected;
    }

    if (pthread_mutex_init(&glock, 0) != 0)
    {
        printf("mutex_init failed on glock.\n");
        exit(2);
    }
    if (pthread_cond_init(&countcond, 0) != 0)
    {
        printf("cond_init failed on glock.\n");
        exit(3);
    }
    // get a priority queue instance
    allq = pq_create();

    // create NPAR remover threads - arg is the pq_t *.
    for (i = 0; i < NPAR; i++)
        if (pthread_create(&tids[i], 0, remover, (void *)allq))
        {
            fprintf(stderr, "failed to create remover thread.\n");
            exit(4);
        }
    // create NPAR inserter threads, with a separate task structure per
    for (i = 0; i < NPAR; i++)
    {
        task_t *t = malloc(sizeof(task_t));
        t->task_indx = i;
        t->task_q = allq;
        if (pthread_create(&tids[i + NPAR], 0, inserter, t))
        {
            fprintf(stderr, "failed to create inserter thread.\n");
            exit(5);
        }
    }
    // wait for count to reach total_items - Note the PATTERN!
    acquire_lock(&glock);
    while (items_removed < total_items)
        slp(&countcond, &glock);
    release_lock(&glock);

    // output the result strings
    for (i = 0; i < NPAR; i++)
    {
        printf("Result string %d: \n    ", i);
        for (j = 0; j < acc[i].rbuf_expected; j++)
        {
            item_t *ip = (item_t *)pq_next(acc[i].rbuf_outq);
            putchar(ip->it_c);
        }
        putchar('\n');
    }
    exit(0);
}
