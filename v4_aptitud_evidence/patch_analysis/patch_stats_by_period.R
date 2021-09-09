library(foreign)
library(tidyr)
library(dplyr)
library(ggplot2)

df1 <- read.dbf("C:/Dropbox (LANCIS)/cambio_cobertura_ca/v4_aptitud_evidence/patch_analysis/result/agro_s1_s3_new_patches_result.dbf")
df2 <- read.dbf("C:/Dropbox (LANCIS)/cambio_cobertura_ca/v4_aptitud_evidence/patch_analysis/result/agro_s3_s5_new_patches_result.dbf")
df3 <- read.dbf("C:/Dropbox (LANCIS)/cambio_cobertura_ca/v4_aptitud_evidence/patch_analysis/result/agro_s5_s6_new_patches_result.dbf")

df4 <- read.dbf("C:/Dropbox (LANCIS)/cambio_cobertura_ca/v4_aptitud_evidence/patch_analysis/result/urb_s1_s3_new_patches_result.dbf")
df5 <- read.dbf("C:/Dropbox (LANCIS)/cambio_cobertura_ca/v4_aptitud_evidence/patch_analysis/result/urb_s3_s5_new_patches_result.dbf")
df6 <- read.dbf("C:/Dropbox (LANCIS)/cambio_cobertura_ca/v4_aptitud_evidence/patch_analysis/result/urb_s5_s6_new_patches_result.dbf")

df1$year <- 2002
df1$prev_year <- 1985
df4$year <- 2002
df4$prev_year <- 1985
df2$year <- 2011
df2$prev_year <- 2002
df5$year <- 2011
df5$prev_year <- 2002
df3$year <- 2014
df3$prev_year <- 2011
df6$year <- 2014
df6$prev_year <- 2011

df1$area_year <- df1$area/(0.0+(df1$year - df1$prev_year))
df2$area_year <- df2$area/(0.0+(df2$year - df2$prev_year))
df3$area_year <- df3$area/(0.0+(df3$year - df3$prev_year))
df4$area_year <- df4$area/(0.0+(df4$year - df4$prev_year))
df5$area_year <- df5$area/(0.0+(df5$year - df5$prev_year))
df6$area_year <- df6$area/(0.0+(df6$year - df6$prev_year))


summarize1 <- df1 %>% group_by(from,expander,year,prev_year) %>% summarize(mean_area_year = mean(area_year, na.rm = TRUE),
                                                            var_area_year = var(area_year, na.rm = TRUE))
summarize2 <- df2 %>% group_by(from,expander,year,prev_year) %>% summarize(mean_area_year = mean(area_year, na.rm = TRUE),
                                                            var_area_year = var(area_year, na.rm = TRUE))
summarize3 <- df3 %>% group_by(from,expander,year,prev_year) %>% summarize(mean_area_year = mean(area_year, na.rm = TRUE),
                                                            var_area_year = var(area_year, na.rm = TRUE))

summarize4 <- df4 %>% group_by(from,expander,year,prev_year) %>% summarize(mean_area_year = mean(area_year),
                                                                           var_area_year = var(area_year))
summarize5 <- df5 %>% group_by(from,expander,year,prev_year) %>% summarize(mean_area_year = mean(area_year, na.rm = TRUE),
                                                                           var_area_year = var(area_year, na.rm = TRUE))
summarize6 <- df6 %>% group_by(from,expander,year,prev_year) %>% summarize(mean_area_year = mean(area_year, na.rm = TRUE),
                                                                           var_area_year = var(area_year, na.rm = TRUE))


patch_stats_agri <- rbind(summarize1, summarize2, summarize3)
patch_stats_agri$to <- 2
patch_stats_agri$to_str <- "Agropecuario"

patch_stats_urb <- rbind(summarize4, summarize5, summarize6)
patch_stats_urb$to <- 4
patch_stats_urb$to_str <- "Urbano"

patch_stats <- rbind(patch_stats_agri, patch_stats_urb)

patch_stats$expander <- patch_stats$expander %>% replace_na(0)   
patch_stats_expander <- patch_stats %>% filter(expander == 1)
patch_stats_patcher <- patch_stats %>% filter(expander == 0)

patch_stats_patcher <- patch_stats_patcher %>% filter(from != 6)
patch_stats_patcher <- patch_stats_patcher %>% filter(from != 4)
patch_stats_expander <- patch_stats_expander %>% filter(from != 6)
patch_stats_expander <- patch_stats_expander %>% filter(from != 4)

patch_stats_expander$transition <- paste0("from_",patch_stats_expander$from,"_to_",patch_stats_expander$to)
patch_stats_patcher$transition <- paste0("from_",patch_stats_patcher$from,"_to_",patch_stats_patcher$to)


#patch_stats_expander_2011 <- patch_stats_expander %>% filter(year <= 2011)


# patch_stats_expander_9 <- patch_stats_expander %>% filter(from == 9)
# patch_stats_patcher_9 <- patch_stats_patcher %>% filter(from == 9)


# id	Clase_v4
# 1	Acuícola
# 2	Agricultura
# 4	Asentamiento humano
# 6	Cuerpo de agua
# 7	Manglar, petén, tular e hidrófila
# 9	Selva
# 11	Sin vegetación
# 14	Duna costera
# 17	ND




ggplot(patch_stats_expander, aes(x = year, y = mean_area_year)) + 
  geom_line(aes(color = transition, linetype = transition),size=1.3)+
  ggtitle("Área promedio de expanción anual (expander)")
 


ggplot(patch_stats_patcher, aes(x = year, y = mean_area_year)) + 
  geom_line(aes(color = transition, linetype = transition),size=1.3)+
  ggtitle("Área promedio de parche nuevo (patcher)")

