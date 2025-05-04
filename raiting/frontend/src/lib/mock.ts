// lib/mock.ts

// lib/mock.ts

export const mockClasses = [
  { id: 1, name: "7А" },
  { id: 2, name: "8Б" },
  { id: 3, name: "9В" },
];

export const mockStudentsByClass = {
  1: [
    {
      id: 1,
      full_name: "Иванов Иван",
      tg_username: "ivan123",
      score: 10,
      total_time: 100,
      answers: [
        { question: "2+2?", answer: "4", correct: true },
        { question: "3+5?", answer: "8", correct: true },
      ],
    },
    {
      id: 2,
      full_name: "Сидорова Анна",
      tg_username: "anna_s",
      score: 8,
      total_time: 120,
      answers: [],
    },
  ],
  2: [
    {
      id: 3,
      full_name: "Петров Петр",
      tg_username: "petrov",
      score: 5,
      total_time: 90,
      answers: [],
    },
  ],
  3: [],
};
