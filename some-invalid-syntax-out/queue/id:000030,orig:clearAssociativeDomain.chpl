enum Counter { one, two, three };
var D : domain ( Counter ) = {Counter.one, Counter.two};
writeln("D has ", D.numIndices, " indices.");
D.clear();
writeln("D has ", D.numIndices, " indices.");
