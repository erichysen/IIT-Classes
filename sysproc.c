#include "types.h"
#include "x86.h"
#include "defs.h"
#include "param.h"
#include "memlayout.h"
#include "mmu.h"
#include "proc.h"

int
sys_fork(void)
{
  return fork();
}

int
sys_exit(void)
{
  exit();
  return 0;  // not reached
}

int
sys_wait(void)
{
  return wait();
}

int
sys_kill(void)
{
  int pid;

  if(argint(0, &pid) < 0)
    return -1;
  return kill(pid);
}

int
sys_getpid(void)
{
  return proc->pid;
}

int
sys_sbrk(void)
{
  int addr;
  int n;

  if(argint(0, &n) < 0)
    return -1;
  addr = proc->sz;
  if(growproc(n) < 0)
    return -1;
  return addr;
}

int
sys_sleep(void)
{
  int n;
  uint ticks0;
  
  if(argint(0, &n) < 0)
    return -1;
  acquire(&tickslock);
  ticks0 = ticks;
  while(ticks - ticks0 < n){
    if(proc->killed){
      release(&tickslock);
      return -1;
    }
    sleep(&ticks, &tickslock);
  }
  release(&tickslock);
  return 0;
}

// return how many clock tick interrupts have occurred
// since start.
int
sys_uptime(void)
{
  uint xticks;
  
  acquire(&tickslock);
  xticks = ticks;
  release(&tickslock);
  return xticks;
}

//MP1 Additions
int
sys_start_burst(void){
	int sb = sys_uptime();
	return sb;
}
int
sys_end_burst(void){
	int eb = sys_uptime();
	return eb;
}
int 
sys_print_bursts(void){
	int i;
	for (i=0; i<100; i++){
		if(proc->burst_array[i] !=0x00){
			cprintf("%d,", proc->burst_array[i]); //print bursts
		}
	}
	cprintf ("Turnaround Time:%d", sys_end_burst() - proc->turn_burst); // print turnaround time
	cprintf("\n");
	return 0;
}
//end mp1 additions

// mp2 additions
int
sys_thread_create(void)
{
	//(void*)tmain
	char *tmain, *stack, *arg;
	argptr(0,&tmain,1);  //line 45 syscall.c
	argptr(1,&stack,0);
	argptr(2,&arg,0);
	return thread_create((void*)tmain, (void*)stack, (void*)arg);
}

int
sys_thread_join(void)
{
	char *stack;
	argptr(0,&stack,1);
	return thread_join((void**)stack);
}

int 
sys_mtx_create(void)
{
	int locked;
	argint(0,&locked);
	return mtx_lock(locked);
}
int
sys_mtx_lock(void)
{
	int lock_id;
	argint(0,&lock_id);
	return mtx_lock(lock_id);
}
int
sys_mtx_unlock(void)
{
	int lock_id;
	argint(0,&lock_id);
	return mtx_unlock(lock_id);
}
//end mp2 additions
