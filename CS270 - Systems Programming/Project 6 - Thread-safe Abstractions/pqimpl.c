#include "pq.h"

// create and initialize a prio queue instance. Return NULL on error.
pq_t *pq_create(void)
{
    // Create priority queue
    pq_t *pqueue = (pq_t *)malloc(sizeof(pq_t));
    if (pqueue == NULL)
    {
        return NULL;
    }

    // Initialize mutex
    if (pthread_mutex_init(&pqueue->lock, NULL) != 0)
    {
        return NULL;
    }

    // Initialize cond
    if (pthread_cond_init(&pqueue->cond, NULL) != 0)
    {
        return NULL;
    }
    pqueue->head = NULL;
    return pqueue;
}

/* This operation never blocks.  Fails (aborts) if OS runs out of memory.
 * N.B. the second argument is the "value" to be stored at the given prio.
 * It will eventually be returned by pq_next() unless it never becomes the
 * highest priority item.  It can be a pointer to anything, or even
 * an integer type.
 */
void pq_insert(pq_t *q, void *item, short prio)
{

    // Create a new item
    struct pq_item_t *new_item = (pq_item_t *)malloc(sizeof(pq_item_t));
    if (new_item == NULL)
    {
        perror("Insufficient Memory.\n");
        exit(0);
    }
    pthread_mutex_lock(&q->lock);
    new_item->item = item;
    new_item->priority = prio;
    new_item->next = NULL;

    // Case where the head has not been initalized
    if (q->head == NULL)
    {
        q->head = new_item;
    }
    else // Compare the priority values
    {

        // The current item's priority is greater than head
        if (prio > q->head->priority)
        {
            // Insert new node before head
            new_item->next = q->head;
            q->head = new_item;
        }
        else
        {
            // Create a new node
            pq_item_t *start = q->head;

            // Traverse the list and find a position to insert new node
            while (start->next != NULL && prio <= start->next->priority)
            {
                start = start->next;
            }
            new_item->next = start->next;
            start->next = new_item;
        }
    }
    pthread_mutex_unlock(&(q->lock));
    pthread_cond_signal(&(q->cond));
}

/* Return the oldest item with highest priority.
 * In other words, the item returns satisfies the predicate:
 * No item in the queue has higher priority AND any item with the same
 * priority was inserted after this item.
 * The calling thread will block if the queue is empty.
 */
void *pq_next(pq_t *q)
{
    pthread_mutex_lock(&q->lock);
    while (q->head == NULL)
    {
        pthread_cond_wait(&q->cond, &q->lock);
    }

    struct pq_item_t *temp = q->head;
    void *retTemp = temp->item;
    q->head = q->head->next;
    free(temp);
    pthread_mutex_unlock(&q->lock);
    return retTemp;
}
