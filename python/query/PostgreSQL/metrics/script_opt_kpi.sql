SELECT 
    COUNT(*) FILTER (WHERE Status = 4)::FLOAT / COUNT(*)::FLOAT AS tasa_cancelacion
FROM Booking;

SELECT 
    AVG(EXTRACT(EPOCH FROM (ModifiedDate - CreatedDate)) / 3600) AS tiempo_promedio_horas
FROM public.Booking
WHERE ModifiedDate IS NOT NULL;

SELECT 
    ChannelType, 
    SUM(CASE WHEN PaidStatus = 1 THEN 1 ELSE 0 END) AS ingresos
FROM public.Booking
GROUP BY ChannelType;

SELECT 
    age, 
    COUNT(*) AS cantidad_pasajeros
FROM public.BookingPassenger
GROUP BY age
ORDER BY age;