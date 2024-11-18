import React, { useState, useEffect, useCallback } from 'react';
import {
  Container,
  Heading,
  SimpleGrid,
  Text,
  useToast,
  Box,
  Input,
  Button
} from '@chakra-ui/react';
import ProductCard from '../components/ProductCard';
import { API_URL } from '../config';

console.log('Home component initialized');

const Home = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const toast = useToast();

  const loadProducts = useCallback(async () => {
    try {
      setLoading(true);
      console.log('Iniciando carga de productos...');
      console.log('API URL:', API_URL);

      const response = await fetch(`${API_URL}/products/`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      console.log('Respuesta de productos recibida:', data);

      if (!data || data.length === 0) {
        console.log('No se encontraron productos');
        toast({
          title: 'Advertencia',
          description: 'No hay productos disponibles',
          status: 'warning',
          duration: 3000,
          isClosable: true,
        });
        setProducts([]);
      } else {
        console.log('Productos cargados exitosamente:', data);
        setProducts(data);
      }
    } catch (error) {
      console.error('Error detallado al cargar productos:', {
        message: error.message,
        name: error.name,
        stack: error.stack
      });

      toast({
        title: 'Error',
        description: 'No se pudieron cargar los productos. Por favor, intente nuevamente.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
      setProducts([]);
    } finally {
      setLoading(false);
    }
  }, [toast]);

  useEffect(() => {
    console.log('Efecto de carga de productos iniciado');
    loadProducts();
  }, [loadProducts]);

  const handleSearch = (event) => {
    setSearchTerm(event.target.value);
    // TODO: Implementar búsqueda de productos
  };

  return (
    <Container maxW="container.xl" py={8}>
      <Box textAlign="center" mb={8}>
        <Heading as="h1" size="2xl" mb={4}>
          Bienvenido a CyberShop
        </Heading>
        <Text fontSize="xl" color="gray.600">
          Descubre nuestros productos más destacados
        </Text>
      </Box>

      <Box mb={4}>
        <Input
          placeholder="Buscar productos..."
          value={searchTerm}
          onChange={handleSearch}
          size="lg"
        />
      </Box>

      {loading ? (
        <Box textAlign="center" py={8}>
          <Text fontSize="xl">Cargando productos...</Text>
        </Box>
      ) : (
        <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6}>
          {products.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </SimpleGrid>
      )}
    </Container>
  );
};

export default Home;
