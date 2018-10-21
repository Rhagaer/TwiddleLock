sort: sort.o
	ld -o sort sort.o
sort.o sort.s
	as -o sort.o sort.s
clean:
	rm *.o sort