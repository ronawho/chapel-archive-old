class C {
  proc foo() { bar(this);
  }
}
proc bar(c: C) { writeln(c); }
var c1: C = new owned C();
c1.foo();
