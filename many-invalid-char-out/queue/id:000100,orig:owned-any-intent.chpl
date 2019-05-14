proc defaultGeneric(arg) {
  writeln(arg.type:string);
}
class SomeClass { }
defaultGeneric(new owned SomeClass());
