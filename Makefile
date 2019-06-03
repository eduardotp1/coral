all: coral

coral.tab.c coral.tab.h:	coral.y
	bison -d coral.y

lex.yy.c: coral.l coral.tab.h
	flex coral.l

coral: lex.yy.c coral.tab.c coral.tab.h
	gcc -o coral coral.tab.c lex.yy.c

clean:
	rm coral coral.tab.c lex.yy.c coral.tab.h