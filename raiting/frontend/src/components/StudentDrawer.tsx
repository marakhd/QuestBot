// components/StudentDrawer.tsx
export default function StudentDrawer({ student, onClose }: any) {
  return (
    <div className="fixed top-0 right-0 w-full md:w-[400px] h-full bg-white shadow-lg z-50 p-6 overflow-y-auto">
      <button onClick={onClose} className="mb-4 text-blue-600">Закрыть</button>
      <h2 className="text-xl font-bold mb-2">{student.full_name}</h2>
      <p className="text-sm text-gray-500">@{student.tg_username}</p>

      <h3 className="mt-4 font-semibold">Ответы:</h3>
      <ul className="mt-2 space-y-2">
        {student.answers.map((a: any, i: any) => (
          <li key={i} className="p-2 rounded bg-gray-100">
            <p className="font-medium">{a.question}</p>
            <p>Ответ: {a.answer} ({a.correct ? "✔" : "✘"})</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
