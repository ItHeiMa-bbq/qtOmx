
#include <stdio.h>

int isNeedNum(int n)
{
    for(int i=2;i<n;i++)
    {
        if(n%i == 0)
        {
            return -1;
        }
        else
        {
            int mul = i*i;
            if(mul > n)
            {
				printf("is num:%d\n",n);
                return n;
            }
        } 
    }
	return -1;
}


int main(int argc,char *argv[])
{
    int num = 0;
    int a = 0;
    int b = 0;
    int count = 0;
    scanf("%d",&num);
    while(getchar() != '\n');
	for(a=num-2;a>=num/2;a--)
	{
		b = num -a ;
        if(isNeedNum(a) != -1 && isNeedNum(b) != -1)
        {
			count++;
        }
    }
    printf("%d\n",count);   
}
