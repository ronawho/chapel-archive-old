var count$: sync int = 0;
cobegin {
  count$ += 1;
  count$ += 1;
  count$ += 1;
}
writeln("count is: ", count$.readFF());
