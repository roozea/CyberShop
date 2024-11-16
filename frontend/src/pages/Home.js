import { Grid, Container, Heading, SimpleGrid } from '@chakra-ui/react';
import { ProductCard } from '../components/ProductCard';

const mockProducts = [
  {
    id: 1,
    name: 'Laptop Gaming Pro',
    price: 999.99,
    image: 'https://via.placeholder.com/300',
    description: 'Potente laptop para gaming con la última tecnología'
  },
  {
    id: 2,
    name: 'Smartphone Ultra',
    price: 599.99,
    image: 'https://via.placeholder.com/300',
    description: 'Smartphone de última generación con cámara profesional'
  },
  {
    id: 3,
    name: 'Tablet Max',
    price: 399.99,
    image: 'https://via.placeholder.com/300',
    description: 'Tablet perfecta para trabajo y entretenimiento'
  },
  {
    id: 4,
    name: 'Smartwatch Pro',
    price: 199.99,
    image: 'https://via.placeholder.com/300',
    description: 'Reloj inteligente con monitoreo de salud'
  }
];

export const Home = () => {
  return (
    <Container maxW="container.xl" py={8}>
      <Heading mb={6}>Productos Destacados</Heading>
      <SimpleGrid columns={{ base: 1, md: 2, lg: 3, xl: 4 }} spacing={6}>
        {mockProducts.map(product => (
          <ProductCard key={product.id} product={product} />
        ))}
      </SimpleGrid>
    </Container>
  );
};
