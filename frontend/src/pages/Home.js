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
import { getProducts } from '../services/api';

const Home = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const toast = useToast();

  const loadProducts = useCallback(async () => {
    try {
      setLoading(true);
      console.log('Fetching products...');
      const data = await getProducts();
      console.log('Products received:', data);
      if (!data || data.length === 0) {
        toast({
          title: 'Advertencia',
          description: 'No hay productos disponibles',
          status: 'warning',
          duration: 3000,
          isClosable: true,
        });
        setProducts([]);
      } else {
        setProducts(data);
      }
    } catch (error) {
      console.error('Error loading products:', error.message, error.response?.data);
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
