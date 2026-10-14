1. ¿Qué campo identifica la muestra?
sample_id

2. ¿Qué once campos consume el modelo?
fixed_acidity,volatile_acidity,citric_acid,residual_sugar,chlorides,free_sulfur_dioxide,total_sulfur_dioxide,density,ph,sulphates,alcohol

3. Proponed una nueva columna que el contrato debería rechazar
Volumen_muestra

4. Proponed dos valores inválidos y explicad por qué
- fixed_acidity: -1.0 (un valor negativo no tiene sentido en el contexto de acidez fija, ya que la acidez no puede ser negativa)
- alcohol: 200.0 (un valor muy alto para el contenido de alcohol en vino, porque la mayoría de los vinos tienen un contenido de alcohol alrededor de un 10%)