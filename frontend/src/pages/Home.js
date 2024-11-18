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
  console.log('Home component rendering');
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const toast = useToast();

  const loadProducts = useCallback(async () => {
    let retryCount = 0;
    const maxRetries = 3;
    const retryDelay = 2000; // 2 segundos

    const attemptLoad = async () => {
      try {
        setLoading(true);
        console.log('Iniciando carga de productos... Intento:', retryCount + 1);
        console.log('API URL:', API_URL);

        const response = await fetch(`${API_URL}/products/`, {
          method: 'GET',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Cache-Control': 'no-cache'
          },
          credentials: 'omit'
        });

        console.log('Respuesta recibida:', {
          status: response.status,
          statusText: response.statusText,
          headers: Object.fromEntries(response.headers.entries())
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Respuesta de productos recibida:', data);

        if (!Array.isArray(data)) {
          throw new Error('La respuesta no es un array de productos');
        }

        if (data.length === 0) {
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
          console.log('Estado de productos actualizado:', data);
        }
        return true; // Éxito
      } catch (error) {
        console.error('Error detallado al cargar productos:', {
          message: error.message,
          name: error.name,
          stack: error.stack,
          url: `${API_URL}/products/`,
          attempt: retryCount + 1
        });

        if (retryCount < maxRetries) {
          console.log(`Reintentando en ${retryDelay}ms...`);
          await new Promise(resolve => setTimeout(resolve, retryDelay));
          retryCount++;
          return false; // Falló, pero podemos reintentar
        }

        toast({
          title: 'Error',
          description: 'No se pudieron cargar los productos. Por favor, intente nuevamente.',
          status: 'error',
          duration: 5000,
          isClosable: true,
        });
        setProducts([]);
        return true; // No más reintentos
      } finally {
        setLoading(false);
      }
    };

    // Intentar cargar hasta que tengamos éxito o agotemos los reintentos
    let success = false;
    while (!success && retryCount <= maxRetries) {
      success = await attemptLoad();
    }
  }, [toast]); // Solo depender del toast

  useEffect(() => {
    console.log('Efecto de carga de productos iniciado');
    loadProducts();
  }, [loadProducts]);

  // Log cuando cambia el estado de productos
  useEffect(() => {
    console.log('Estado de productos actualizado:', products);
  }, [products]);

  const handleSearch = (event) => {
    setSearchTerm(event.target.value);
    // TODO: Implementar búsqueda de productos
  };

  console.log('Renderizando componente Home:', { loading, productsLength: products.length });

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
          {products && products.length > 0 ? (
            products.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))
          ) : (
            <Box textAlign="center" py={8}>
              <Text fontSize="xl">No hay productos disponibles</Text>
            </Box>
          )}
        </SimpleGrid>
      )}
    </Container>
  );
};

export default Home;
