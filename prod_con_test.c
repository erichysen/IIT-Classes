#include"types.h"
#include"user.h"
struct yard 
{
	int trees;
	int stumps;
	int acre[15]; //its a prarie 1 tree||stump per acre.
}yard;

static int mutex;

//plant trees in acres where there are stumps 
//producer
void plant_trees (void*arg)
{
	int i, j;  
	j = 0;
	for(i = 0; i < 15; i++)
	{
		yard.stumps = 15;
		mtx_lock(mutex);
		if(yard.stumps == 0)
		{
			mtx_unlock(mutex);
			sleep(1);
		} 
		else 
		{
			if(yard.acre[j] == 0)
			{
				//printf("Planted tree in acre %d\n", i);
				printf(1,"Planted tree in acre %d\n", i);
				yard.acre[j] = i;
				yard.trees ++;
				yard.stumps --;
			}
			j++;
			mtx_unlock(mutex);
		}
	}
	exit();
}

//chops trees that have been planted
//consumer
void chop_trees (void*arg)
{
	int i,j;
	int spot;
	spot =0; 
	for(j=0; j < sizeof(yard.acre); j++)
	{
		if(yard.acre[j]!=0)
		{
			spot =  spot +1;
		}		
	}
	for(i = 0; i < 15; i++)
	{
		mtx_lock(mutex);
		if(yard.trees == 0)
		{
			mtx_unlock(mutex);
			sleep(10); //force c switch
		}	 
		else 
		{
			if(spot>=0)
			{
				//printf("Chopped tree in acre %d\n", yard.acre[spot]);
				printf(1,"Chopped tree in acre %d\n", yard.acre[spot]);
				yard.acre[spot] = 0;
				yard.trees --;
				yard.stumps ++;
			}
			spot--;
			mtx_unlock(mutex);
		}
	}
	exit();
}

int main(int argc, char**argv)
{
	mutex = mtx_create(0);
	uint* stack = malloc(1024); //stack size 1024 (assumed)
	thread_create(*plant_trees,stack,(void*)0); //producer thread
	thread_join((void*)0);
	thread_create(*chop_trees,stack,(void*)0);  //consumer thread
	thread_join((void*)1);                      
	exit();
	return 0;
}