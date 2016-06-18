#include "syscall.h"
#include "traps.h"

#define SYSCALL(name) \
  .globl name; \
  name: \
    movl $SYS_ ## name, %eax; \
    int $T_SYSCALL; \
    ret

SYSCALL(fork)
SYSCALL(exit)
SYSCALL(wait)
SYSCALL(pipe)
SYSCALL(read)
SYSCALL(write)
SYSCALL(close)
SYSCALL(kill)
SYSCALL(exec)
SYSCALL(open)
SYSCALL(mknod)
SYSCALL(unlink)
SYSCALL(fstat)
SYSCALL(link)
SYSCALL(mkdir)
SYSCALL(chdir)
SYSCALL(dup)
SYSCALL(getpid)
SYSCALL(sbrk)
SYSCALL(sleep)
SYSCALL(uptime)
//MP1 Additions
SYSCALL(start_burst)
SYSCALL(end_burst)
SYSCALL(print_bursts)
//End MP1 Additions
//MP2 Additions
SYSCALL(thread_create)
SYSCALL(thread_join)
SYSCALL(mtx_create)
SYSCALL(mtx_lock)
SYSCALL(mtx_unlock)
//End mp2 additions