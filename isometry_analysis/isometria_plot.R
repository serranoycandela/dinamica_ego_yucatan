similitud <- read.csv("~/Desktop/similitud.csv")
barplot(height=similitud$promedio, names=similitud$isometry)
# Load ggplot2
library(ggplot2)

# Barplot
names(similitud) <- c("Isometría", "Similitud")
ggplot(similitud, aes(x=Isometría, y=Similitud)) + 
  geom_bar(stat = "identity")
