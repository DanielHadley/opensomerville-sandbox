attend <- read.csv("~/Dev/opensomerville-sandbox/attendance.csv")

for (b in levels(attend$board))
{
  cat(b, '\n')
  a=subset(attend, board==b)
  a$name = factor(a$name)
  a$status = factor(a$status)
  with(a, print(table(name, status)))

  cat('\n\n')
}