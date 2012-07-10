use driver_domains;

const bigDom4D = Dom4D.expand((1,1,1,1));
var A: [bigDom4D] 4*int = {(...bigDom4D.dims())};
var B: [Dom4D] 4*int;

resetCommDiagnostics();
startCommDiagnostics();
B = A[1..n4,1..n4,1..n4,1..n4];
stopCommDiagnostics();
writeln(getCommDiagnostics());
for i in Dom4D do if B[i]!=i then writeln("ERROR: B[", i, "]==", B[i]);
