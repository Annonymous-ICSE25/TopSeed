/^# Packages using this file: / {
  s/# Packages using this file://
  ta
  :a
  s/ gcal / gcal /
  tb
  s/ $/ gcal /
  :b
  s/^/# Packages using this file:/
}
