library(tidyverse)
library(writexl)


#-------ESTA PARTE DEL CÓDIGO TE AYUDA A EXTRAER LAS ACTIVACIONES DE LAS UNIDADES M'1 y M'2--------------------

read_and_combine_files <- function(folder_num) {
  path_base <- "C:/Users/migue/Documents/Psicología/Estudio doctorado/Simulación/XAY data/FaseA-Prueba"
  
  # Construye las rutas de los archivos
  file1_path <- paste0(path_base, "/R1-SC-", folder_num, "/XY/Acts/14(mot,r)")
  file2_path <- paste0(path_base, "/R1-SC-", folder_num, "/XY/Acts/16(mot,r)")
  
  # Lee los archivos
  file1_data <- read_lines(file1_path)
  file2_data <- read_lines(file2_path)
  
  # Crea un tibble
  data <- tibble(
    Folder = paste0("R1-SC-", folder_num),
    ColumnA = file1_data,
    ColumnB = file2_data
  )
  
  return(data)
}

all_data <- map_df(1:10, read_and_combine_files)

averages_per_folder <- all_data %>%
  group_by(Folder) %>%
  summarise(
    Avg_ColumnA = mean(as.numeric(ColumnA), na.rm = TRUE),
    Avg_ColumnB = mean(as.numeric(ColumnB), na.rm = TRUE)
  )

print(averages_per_folder)
print(all_data, n=250)


#--------ESTA PARTE DEL CODIGO TE AYUDA A EXTRAER LOS PESOS DE TODAS LAS UNIDADES----------------------------------

# Función para leer y calcular el promedio de un archivo en 'Wgts'
read_and_avg_wgts_file <- function(base_path, folder_num, subfolder, file) {
  # Construye la ruta del archivo
  file_path <- file.path(base_path, paste0("R1-SC-", folder_num), "XY", "Wgts", subfolder, file)
  
  # Lee el archivo si existe y calcula su promedio, de lo contrario devuelve NA
  if(file.exists(file_path)) {
    data <- read_lines(file_path)
    avg_data <- mean(as.numeric(data), na.rm = TRUE)
  } else {
    avg_data <- NA
  }
  
  # Crea un tibble
  tibble(
    Folder = paste0("R1-SC-", folder_num),
    Subfolder = subfolder,
    File = file,
    AvgData = avg_data
  )
}

# Mapa de subcarpetas a archivos
file_map <- list(
  "4(sen,e)" = "Pre1(1,sen,s)",
  "5(sen,H)" = "Pre1(4,sen,e)",
  "6(sen,e)" = "Pre1(2,sen,s)",
  "7(sen,H)" = "Pre1(6,sen,e)",
  "8(sen,e)" = "Pre1(3,sen,s)",
  "9(sen,H)" = "Pre1(8,sen,e)",
  "10(mot,e)" = "Pre1(4,sen,e)",
  "11(mot,e)" = "Pre1(6,sen,e)",
  "12(mot,e)" = "Pre1(8,sen,e)",
  "14(mot,r)" = "Pre1(10,mot,e)",
  "15(mot,r)" = "Pre1(11,mot,e)",
  "16(mot,r)" = "Pre1(12,mot,e)"
)

# Para el caso especial de "13(mot,D)"
file_map_special <- list(
  "13(mot,D)" = c("Pre1(10,mot,e)", "Pre2(11,mot,e)", "Pre3(12,mot,e)")
)

# Base path
base_path <- "C:/Users/migue/Documents/Psicología/Estudio doctorado/Simulación/XAY data/FaseA-Prueba"

# Iterar sobre todas las carpetas y subcarpetas
results <- map_df(1:10, function(folder_num) {
  
  regular_files <- map2_df(names(file_map), file_map, ~read_and_avg_wgts_file(base_path, folder_num, .x, .y))
  
  special_files <- map2_df(names(file_map_special), file_map_special, function(sf, files) {
    map_df(files, ~read_and_avg_wgts_file(base_path, folder_num, sf, .x))
  })
  
  bind_rows(regular_files, special_files)
})

# Visualizar los resultados
print(results, n=200)
write_xlsx(results, "C:/Users/migue/Documents/Psicología/Estudio doctorado/Simulación/XAY data/FaseA-Prueba/results.xlsx")



