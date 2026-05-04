import React from "react";
import { FaFireAlt } from "react-icons/fa"; // 🔥 Install react-icons if not already

const Card = ({ title, value }) => {
  return (
    <div className="group relative p-6 bg-white dark:bg-gray-800 shadow-md rounded-lg border border-transparent hover:border-red-400 transition duration-300 hover:shadow-xl overflow-hidden fire-up-card">
      <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-200">{title}</h3>
      <div className="flex items-center gap-2 mt-2">
        <p className="text-3xl font-bold text-red-600 group-hover:scale-105 transition-transform duration-200">
          {value}
        </p>
        <FaFireAlt className="text-orange-500 text-xl animate-pulse group-hover:animate-bounce" />
      </div>
      <div className="fire-glow"></div>
    </div>
  );
};

export default Card;
