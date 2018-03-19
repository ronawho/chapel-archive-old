
proc myproc() {
  var loc = Locales[0];
  coforall 1..1 do on loc { writeln("hi"); }
}

myproc();
