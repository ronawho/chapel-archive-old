class C {
  type elementType;
  type indexType;
  type containerType;
}
class Container {
  type containedType;
}
proc f(c: C(real,?t,?u)) {
  // ...
}
proc g(c: C(?t,?u,Container)) {
  // ...
}
var cc = new borrowed Container(int);
var c = new borrowed C(real, int, cc.type);
f(c);
g(c);