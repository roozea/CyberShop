import {
  Container,
  Heading,
  SimpleGrid,
  Box,
  Input,
  Select,
  Button,
  Flex,
  Text,
  Badge,
  useToast
} from '@chakra-ui/react';
import { ProductCard } from '../components/ProductCard';
import { useState, useEffect, useCallback } from 'react';
import { getProducts, searchProducts, addToCart as apiAddToCart } from '../services/api';

export const Home = () => {
  const [products, setProducts] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('Todas');
  const [loading, setLoading] = useState(true);
  const toast = useToast();

  const categories = [
    'Todas', 'Laptops', 'Smartphones', 'Tablets', 'Wearables',
    'Audio', 'Cámaras', 'Monitores', 'Consolas'
  ];

  const loadProducts = useCallback(async () => {
    try {
      setLoading(true);
      const data = await getProducts();
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
      console.error('Error loading products:', error);
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

  const handleSearch = async () => {
    try {
      setLoading(true);
      const data = await searchProducts(searchTerm);
      setProducts(data);
    } catch (error) {
      console.error('Error searching products:', error);
      toast({
        title: 'Error',
        description: 'Error al buscar productos',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    } finally {
      setLoading(false);
    }
  };

  const handleAddToCart = async (product) => {
    try {
      await apiAddToCart({ productId: product.id, quantity: 1 });
      toast({
        title: 'Producto agregado',
        description: `${product.name} ha sido agregado al carrito`,
        status: 'success',
        duration: 3000,
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

  const filteredProducts = products.filter(product => {
    const matchesCategory = selectedCategory === 'Todas' || product.category === selectedCategory;
    return matchesCategory;
  });

  return (
    <Box>
      {/* Banner Promocional */}
      <Box
        bgImage="url('https://images.unsplash.com/photo-1550745165-9bc0b252726f')"
        bgPosition="center"
        bgSize="cover"
        h="300px"
        position="relative"
        mb={8}
      >
        <Box
          position="absolute"
          top="0"
          left="0"
          right="0"
          bottom="0"
          bg="rgba(0,0,0,0.6)"
          display="flex"
          alignItems="center"
          justifyContent="center"
          flexDirection="column"
          color="white"
          textAlign="center"
          p={4}
        >
          <Heading size="2xl" mb={4}>Mega Ofertas CyberShop</Heading>
          <Text fontSize="xl" maxW="container.md">
            Descubre las mejores ofertas en tecnología. Hasta 50% de descuento en productos seleccionados.
          </Text>
          <Button colorScheme="blue" size="lg" mt={6}>
            Ver Ofertas
          </Button>
        </Box>
      </Box>

      <Container maxW="container.xl" py={8}>
        {/* Filtros y Búsqueda */}
        <Flex mb={8} gap={4} flexWrap={{ base: 'wrap', md: 'nowrap' }}>
          <Input
            placeholder="Buscar productos..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
            flex={1}
          />
          <Button onClick={handleSearch} colorScheme="blue">
            Buscar
          </Button>
          <Select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            width={{ base: '100%', md: '200px' }}
          >
            {categories.map(category => (
              <option key={category} value={category}>{category}</option>
            ))}
          </Select>
        </Flex>

        {/* Productos */}
        <Box mb={8}>
          <Flex justify="space-between" align="center" mb={6}>
            <Heading size="lg">Productos Destacados</Heading>
            <Badge colorScheme="green" p={2} borderRadius="md">
              {filteredProducts.length} productos encontrados
            </Badge>
          </Flex>

          {loading ? (
            <Text>Cargando productos...</Text>
          ) : (
            <SimpleGrid columns={{ base: 1, md: 2, lg: 3, xl: 4 }} spacing={6}>
              {filteredProducts.map(product => (
                <ProductCard
                  key={product.id}
                  product={product}
                  onAddToCart={() => handleAddToCart(product)}
                />
              ))}
            </SimpleGrid>
          )}
        </Box>

        {/* Categorías Destacadas */}
        <Box>
          <Heading size="lg" mb={6}>Categorías Populares</Heading>
          <SimpleGrid columns={{ base: 2, md: 3, lg: 4 }} spacing={6}>
            {categories.slice(1).map(category => (
              <Box
                key={category}
                bg="gray.100"
                p={4}
                borderRadius="lg"
                cursor="pointer"
                _hover={{ bg: 'blue.50' }}
                onClick={() => setSelectedCategory(category)}
              >
                <Text fontSize="lg" fontWeight="bold" textAlign="center">
                  {category}
                </Text>
              </Box>
            ))}
          </SimpleGrid>
        </Box>
      </Container>
    </Box>
  );
};
