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
        bgGradient="linear(to-r, teal.500, blue.500)"
        color="white"
        py={16}
        px={4}
        borderRadius="xl"
        boxShadow="2xl"
        position="relative"
        overflow="hidden"
        _before={{
          content: '""',
          position: "absolute",
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          bgGradient: "linear(to-r, blackAlpha.300, blackAlpha.500)",
          zIndex: 0,
        }}
      >
        <Box position="relative" zIndex={1}>
          <Heading as="h1" size="2xl" mb={6} textShadow="2px 2px 4px rgba(0,0,0,0.3)">
            Bienvenido a CyberShop
          </Heading>
          <Text fontSize="2xl" mb={8} textShadow="1px 1px 2px rgba(0,0,0,0.2)">
            Descubre nuestros productos más destacados con las mejores ofertas
          </Text>
          <Button
            size="lg"
            colorScheme="white"
            variant="outline"
            _hover={{
              transform: "translateY(-2px)",
              boxShadow: "xl",
            }}
            transition="all 0.2s"
          >
            Ver Ofertas Especiales
          </Button>
        </Box>
      </Box>

      <Box
        mb={8}
        p={6}
        bg="white"
        borderRadius="xl"
        boxShadow="xl"
        position="relative"
        _before={{
          content: '""',
          position: "absolute",
          top: 0,
          left: 0,
          right: 0,
          height: "2px",
          bgGradient: "linear(to-r, teal.500, blue.500)",
        }}
      >
        <Input
          placeholder="Buscar productos..."
          value={searchTerm}
          onChange={handleSearch}
          size="lg"
          bg="white"
          _focus={{
            borderColor: "teal.400",
            boxShadow: "0 0 0 1px teal.400",
          }}
        />
      </Box>

      {loading ? (
        <Box
          textAlign="center"
          py={12}
          bg="white"
          borderRadius="xl"
          boxShadow="xl"
        >
          <Text fontSize="xl" color="gray.600">Cargando productos...</Text>
        </Box>
      ) : (
        <SimpleGrid
          columns={{ base: 1, sm: 2, md: 3, lg: 4 }}
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
              borderRadius="xl"
              boxShadow="xl"
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
