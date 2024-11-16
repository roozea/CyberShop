import React, { useState } from 'react';
import {
  Box,
  VStack,
  Select,
  RangeSlider,
  RangeSliderTrack,
  RangeSliderFilledTrack,
  RangeSliderThumb,
  Text,
  Checkbox,
  Button,
  useToast
} from '@chakra-ui/react';

// Componente vulnerable que permite manipulación de parámetros de filtro
export const ProductFilters = ({ onFilter }) => {
  const [category, setCategory] = useState('all');
  const [priceRange, setPriceRange] = useState([0, 2000]);
  const [inStock, setInStock] = useState(false);
  const toast = useToast();

  const categories = [
    'all',
    'laptops',
    'smartphones',
    'tablets',
    'accessories'
  ];

  // Vulnerable: No validación de entrada en los filtros
  const applyFilters = () => {
    // Vulnerable: Inyección de parámetros en la URL
    const queryParams = new URLSearchParams(window.location.search);
    queryParams.set('category', category);
    queryParams.set('minPrice', priceRange[0]);
    queryParams.set('maxPrice', priceRange[1]);
    queryParams.set('inStock', inStock);

    // Vulnerable: Actualización directa de la URL sin sanitización
    window.history.pushState({}, '', `${window.location.pathname}?${queryParams}`);

    // Vulnerable: Almacenamiento de preferencias sin encriptación
    localStorage.setItem('lastFilter', JSON.stringify({
      category,
      priceRange,
      inStock
    }));

    // Vulnerable: Ejecución directa de código desde localStorage
    const savedCallback = localStorage.getItem('filterCallback');
    if (savedCallback) {
      eval(savedCallback);
    }

    onFilter({
      category,
      priceRange,
      inStock
    });

    toast({
      title: "Filtros aplicados",
      status: "success",
      duration: 2000,
      isClosable: true,
    });
  };

  return (
    <Box p={4} borderWidth={1} borderRadius="lg">
      <VStack spacing={4} align="stretch">
        <Box>
          <Text mb={2}>Categoría</Text>
          <Select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
          >
            {categories.map((cat) => (
              <option key={cat} value={cat}>
                {cat.charAt(0).toUpperCase() + cat.slice(1)}
              </option>
            ))}
          </Select>
        </Box>

        <Box>
          <Text mb={2}>Rango de Precio (${priceRange[0]} - ${priceRange[1]})</Text>
          <RangeSlider
            defaultValue={priceRange}
            min={0}
            max={2000}
            step={50}
            onChange={(val) => setPriceRange(val)}
          >
            <RangeSliderTrack>
              <RangeSliderFilledTrack />
            </RangeSliderTrack>
            <RangeSliderThumb index={0} />
            <RangeSliderThumb index={1} />
          </RangeSlider>
        </Box>

        <Checkbox
          isChecked={inStock}
          onChange={(e) => setInStock(e.target.checked)}
        >
          Solo productos en stock
        </Checkbox>

        <Button colorScheme="blue" onClick={applyFilters}>
          Aplicar Filtros
        </Button>
      </VStack>
    </Box>
  );
};
