import React from 'react';
import {
  Box,
  Text,
  Stack,
  Avatar,
  Flex,
  StarIcon,
  Button,
  Textarea,
  useToast
} from '@chakra-ui/react';

// Componente vulnerable que permite XSS a través de las reseñas
export const Reviews = ({ productId }) => {
  const [reviews, setReviews] = React.useState([
    {
      id: 1,
      user: "Usuario1",
      rating: 4,
      comment: "¡Excelente producto!",
      date: "2024-01-15"
    },
    {
      id: 2,
      user: "Usuario2",
      rating: 5,
      comment: "Muy recomendado",
      date: "2024-01-16"
    }
  ]);
  const [newReview, setNewReview] = React.useState("");
  const toast = useToast();

  // Función vulnerable que no sanitiza el input
  const addReview = () => {
    const review = {
      id: reviews.length + 1,
      user: "Usuario" + (reviews.length + 1),
      rating: Math.floor(Math.random() * 5) + 1,
      comment: newReview,
      date: new Date().toISOString().split('T')[0]
    };

    setReviews([...reviews, review]);
    // Vulnerable: Se inserta directamente el HTML sin sanitizar
    document.getElementById('reviews-container').innerHTML += `
      <div class="review">
        <p>${review.comment}</p>
      </div>
    `;
    setNewReview("");

    toast({
      title: "Reseña agregada",
      status: "success",
      duration: 3000,
      isClosable: true,
    });
  };

  return (
    <Box p={4}>
      <Text fontSize="xl" mb={4}>Reseñas del Producto</Text>
      <Box id="reviews-container">
        {reviews.map((review) => (
          <Box key={review.id} p={4} borderWidth={1} borderRadius="md" mb={4}>
            <Flex align="center" mb={2}>
              <Avatar size="sm" name={review.user} mr={2} />
              <Text fontWeight="bold">{review.user}</Text>
            </Flex>
            <Text mb={2}>{review.comment}</Text>
            <Flex>
              {Array(5).fill("").map((_, i) => (
                <Box
                  key={i}
                  color={i < review.rating ? "yellow.400" : "gray.300"}
                >
                  ★
                </Box>
              ))}
            </Flex>
            <Text fontSize="sm" color="gray.500">{review.date}</Text>
          </Box>
        ))}
      </Box>
      <Stack spacing={3} mt={4}>
        <Textarea
          value={newReview}
          onChange={(e) => setNewReview(e.target.value)}
          placeholder="Escribe tu reseña..."
        />
        <Button colorScheme="blue" onClick={addReview}>
          Agregar Reseña
        </Button>
      </Stack>
    </Box>
  );
};
