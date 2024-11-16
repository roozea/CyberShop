import {
  Grid,
  Container,
  Heading,
  SimpleGrid,
  Box,
  Input,
  Select,
  Button,
  Flex,
  Image,
  Text,
  Badge,
  Stack,
  useToast
} from '@chakra-ui/react';
import { ProductCard } from '../components/ProductCard';
import { ProductFilters } from '../components/ProductFilters';
import { useState } from 'react';

const mockProducts = [
  {
    id: 1,
    name: 'Laptop Gaming Pro X',
    price: 999.99,
    image: 'https://images.unsplash.com/photo-1603302576837-37561b2e2302',
    description: 'Potente laptop gaming con RTX 4080, 32GB RAM, 1TB SSD',
    category: 'Laptops',
    rating: 4.5,
    stock: 15,
    discount: 10
  },
  {
    id: 2,
    name: 'Smartphone Ultra 5G',
    price: 799.99,
    image: 'https://images.unsplash.com/photo-1592899677977-9c10ca588bbd',
    description: 'Smartphone flagship con cámara 108MP, 256GB',
    category: 'Smartphones',
    rating: 4.8,
    stock: 20,
    discount: 15
  },
  {
    id: 3,
    name: 'Tablet Pro Max',
    price: 599.99,
    image: 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0',
    description: 'Tablet profesional con M2, perfecta para creativos',
    category: 'Tablets',
    rating: 4.6,
    stock: 8,
    discount: 0
  },
  {
    id: 4,
    name: 'Smartwatch Elite',
    price: 299.99,
    image: 'https://images.unsplash.com/photo-1579586337278-3befd40fd17a',
    description: 'Reloj inteligente con ECG, GPS y monitor de sueño',
    category: 'Wearables',
    rating: 4.7,
    stock: 12,
    discount: 20
  },
  {
    id: 5,
    name: 'Auriculares Pro ANC',
    price: 249.99,
    image: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e',
    description: 'Auriculares premium con cancelación de ruido',
    category: 'Audio',
    rating: 4.9,
    stock: 25,
    discount: 5
  },
  {
    id: 6,
    name: 'Cámara DSLR 4K',
    price: 1299.99,
    image: 'https://images.unsplash.com/photo-1516035069371-29a1b244cc32',
    description: 'Cámara profesional para fotografía y video',
    category: 'Cámaras',
    rating: 4.8,
    stock: 5,
    discount: 0
  },
  {
    id: 7,
    name: 'Monitor Gaming 240Hz',
    price: 449.99,
    image: 'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf',
    description: 'Monitor gaming QHD con 1ms de respuesta',
    category: 'Monitores',
    rating: 4.6,
    stock: 10,
    discount: 12
  },
  {
    id: 8,
    name: 'Consola Next-Gen',
    price: 499.99,
    image: 'https://images.unsplash.com/photo-1486401899868-0e435ed85128',
    description: 'Consola de última generación con ray-tracing',
    category: 'Consolas',
    rating: 4.9,
    stock: 3,
    discount: 0
  }
];

const categories = [
  'Todas', 'Laptops', 'Smartphones', 'Tablets', 'Wearables',
  'Audio', 'Cámaras', 'Monitores', 'Consolas'
];

export const Home = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('Todas');
  const toast = useToast();

  const filteredProducts = mockProducts.filter(product => {
    const matchesSearch = product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         product.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === 'Todas' || product.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const handleAddToCart = (product) => {
    toast({
      title: 'Producto agregado',
      description: `${product.name} ha sido agregado al carrito`,
      status: 'success',
      duration: 3000,
      isClosable: true,
    });
  };

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
            flex={1}
          />
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

          <SimpleGrid columns={{ base: 1, md: 2, lg: 3, xl: 4 }} spacing={6}>
            {filteredProducts.map(product => (
              <ProductCard
                key={product.id}
                product={product}
                onAddToCart={() => handleAddToCart(product)}
              />
            ))}
          </SimpleGrid>
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
