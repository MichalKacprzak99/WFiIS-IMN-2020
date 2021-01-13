CXX = g++
EXEC = main.exe
CXXFLAGS = -std=c++17 -O2
LIBS = -lm

SRC=$(wildcard *.cpp)
OBJS=$(SRC:.cpp=.o)
DEPS=$(SRC:.cpp=.d)

$(EXEC): $(OBJS) 
	$(CXX) $(CXXFLAGS) $+ -o $@


*.o: *.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

.PHONY: clean run rebuild

rebuild: 
	make clean
	make run

clean:
	rm -f *.o
	rm -f *~
	rm -f *.d
	rm -f *.d
	rm -r result
	rm -r images
	rm -f $(EXEC)

run: $(EXEC)
	mkdir result
	mkdir images
	./$(EXEC)
	gnuplot plot.sh


