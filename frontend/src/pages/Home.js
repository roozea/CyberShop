import React, { useState, useEffect, useCallback } from 'react';
import {
  Container,
  Heading,
  SimpleGrid,
  Text,
  useToast,
  Box,
  Button
} from '@chakra-ui/react';
import ProductCard from '../components/ProductCard';
import { getProducts, searchProducts, addToCart as apiAddToCart } from '../services/api';

const Home = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const toast = useToast();

  const categories = [
    "Electronics",
    "Accessories",
    "Gaming"
  ];

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

  const handleSearch = async (term) => {
    setSearchTerm(term);
    if (!term) {
      loadProducts();
      return;
    }
    try {
      const results = await searchProducts(term);
      setProducts(results);
    } catch (error) {
      console.error('Error searching products:', error);
      toast({
        title: 'Error',
        description: 'Error al buscar productos',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    }
  };

  const handleAddToCart = async (productId) => {
    try {
      await apiAddToCart({ productId, quantity: 1 });
      toast({
        title: 'Éxito',
        description: 'Producto agregado al carrito',
        status: 'success',
        duration: 2000,
        isClosable: true,
      });
    } catch (error) {
      console.error('Error adding to cart:', error);
      toast({
        title: 'Error',
        description: 'No se pudo agregar el producto al carrito',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    }
  };

  const filteredProducts = products.filter(product =>
    (!selectedCategory || product.category === selectedCategory)
  );

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

      {/* Categorías */}
      <Box mb={8}>
        <Heading as="h2" size="lg" mb={4}>
          Categorías Populares
        </Heading>
        <SimpleGrid columns={{ base: 1, md: 3 }} spacing={4}>
          {categories.map((category) => (
            <Button
              key={category}
              size="lg"
              variant={selectedCategory === category ? "solid" : "outline"}
              onClick={() => setSelectedCategory(category === selectedCategory ? '' : category)}
            >
              {category}
            </Button>
          ))}
        </SimpleGrid>
      </Box>

      {/* Productos */}
      <Box>
        <Heading as="h2" size="lg" mb={4}>
          Productos Destacados
        </Heading>
        {loading ? (
          <Text>Cargando productos...</Text>
        ) : (
          <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6}>
            {filteredProducts.map((product) => (
              <ProductCard
                key={product.id}
                product={product}
                onAddToCart={() => handleAddToCart(product.id)}
              />
            ))}
          </SimpleGrid>
        )}
        {!loading && filteredProducts.length === 0 && (
          <Text textAlign="center" fontSize="lg" color="gray.600">
            No se encontraron productos en esta categoría
          </Text>
        )}
      </Box>

      {/* Categorías destacadas con imágenes */}
      <Box mt={12}>
        <Heading as="h2" size="lg" mb={6}>
          Explora por Categoría
        </Heading>
        <SimpleGrid columns={{ base: 1, md: 3 }} spacing={8}>
          {categories.map((category) => (
            <Box
              key={category}
              borderRadius="lg"
              overflow="hidden"
              bg="gray.100"
              p={6}
              textAlign="center"
              cursor="pointer"
              onClick={() => setSelectedCategory(category)}
              _hover={{ transform: 'scale(1.02)', transition: 'transform 0.2s' }}
            >
              <Heading size="md">{category}</Heading>
              <Text mt={2} color="gray.600">
                Explora {category}
              </Text>
            </Box>
          ))}
        </SimpleGrid>
      </Box>
    </Container>
  );
};

export default Home;
