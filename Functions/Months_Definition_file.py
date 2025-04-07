def months_convert(Jan_2025,Feb_2025,Mar_2025):
    Jan_2025 = Jan_2025.iloc[:, 0:8]
    Jan_2025 = Jan_2025.fillna(0)
    Feb_2025 = Feb_2025.iloc[:, 0:8]
    Feb_2025 = Feb_2025.fillna(0)
    Mar_2025 = Mar_2025.iloc[:, 0:8]
    Mar_2025 = Mar_2025.fillna(0)
    
    return Jan_2025, Feb_2025, Mar_2025