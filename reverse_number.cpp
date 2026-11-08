#include <iostream.h>
#include <conio.h>
# include <stdio.h>
void main(){
clrscr();
long a,b,c,d,e,f,g,h,n;
cout<< "enter a number of the five digit" ;
cin >>n;
a=n/10000;
b=n%10000;
c=b/1000;
d=b%1000;
e=d/100;
f=d%100;
g=f/10;
h=f%10;
cout<<"five digite number ";
cout << "\n this is the reverse of the five digit number "  << h<<g<<e<<c<<a;
   getchar();
   }
