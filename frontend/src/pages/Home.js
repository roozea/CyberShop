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
import api from '../services/api';

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

        const response = await api.get('/products/');
        console.log('Respuesta de productos recibida:', response.data);

        if (!Array.isArray(response.data)) {
          throw new Error('La respuesta no es un array de productos');
        }

        if (response.data.length === 0) {
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
          console.log('Productos cargados exitosamente:', response.data);
          setProducts(response.data);
          toast({
            title: 'Éxito',
            description: `${response.data.length} productos cargados`,
            status: 'success',
            duration: 3000,
            isClosable: true,
          });
        }
        return true; // Éxito
      } catch (error) {
        console.error('Error detallado al cargar productos:', {
          message: error.message,
          name: error.name,
          stack: error.stack,
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
        console.log('Carga finalizada');
      }
    };

    // Intentar cargar hasta que tengamos éxito o agotemos los reintentos
    let success = false;
    while (!success && retryCount <= maxRetries) {
      success = await attemptLoad();
    }
  }, [toast]);

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
      <Box
        textAlign="center"
        mb={8}
        bgGradient="linear(to-r, blue.400, purple.500)"
        color="white"
        py={12}
        px={4}
        borderRadius="lg"
        boxShadow="xl"
      >
        <Heading as="h1" size="2xl" mb={4}>
          Bienvenido a CyberShop
        </Heading>
        <Text fontSize="xl">
          Descubre nuestros productos más destacados con las mejores ofertas
        </Text>
      </Box>

      <Box
        mb={8}
        p={6}
        bg="white"
        borderRadius="lg"
        boxShadow="md"
      >
        <Input
          placeholder="Buscar productos..."
          value={searchTerm}
          onChange={handleSearch}
          size="lg"
          bg="white"
          _focus={{
            borderColor: "blue.400",
            boxShadow: "0 0 0 1px blue.400"
          }}
        />
      </Box>

      {loading ? (
        <Box
          textAlign="center"
          py={12}
          bg="white"
          borderRadius="lg"
          boxShadow="md"
        >
          <Text fontSize="xl" color="gray.600">Cargando productos...</Text>
        </Box>
      ) : (
        <SimpleGrid
          columns={{ base: 1, md: 2, lg: 3 }}
          spacing={8}
          px={4}
        >
          {products && products.length > 0 ? (
            products.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))
          ) : (
            <Box
              textAlign="center"
              py={12}
              bg="white"
              borderRadius="lg"
              boxShadow="md"
              gridColumn="1 / -1"
            >
              <Text fontSize="xl" color="gray.600">No hay productos disponibles</Text>
            </Box>
          )}
        </SimpleGrid>
      )}
    </Container>
  );
};

export default Home;
