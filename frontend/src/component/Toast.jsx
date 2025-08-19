import React, { useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { FaCheckCircle, FaExclamationTriangle, FaTimes } from "react-icons/fa";

const Toast = ({ message, type = "success", onClose, duration = 3000 }) => {
  useEffect(() => {
    const timer = setTimeout(() => {
      onClose();
    }, duration);

    return () => clearTimeout(timer);
  }, [duration, onClose]);

  const getToastStyles = () => {
    switch (type) {
      case "success":
        return {
          bg: "bg-green-50",
          border: "border-green-200",
          text: "text-green-700",
          icon: <FaCheckCircle className="h-5 w-5 text-green-500" />,
        };
      case "error":
        return {
          bg: "bg-red-50",
          border: "border-red-200",
          text: "text-red-700",
          icon: <FaExclamationTriangle className="h-5 w-5 text-red-500" />,
        };
      default:
        return {
          bg: "bg-blue-50",
          border: "border-blue-200",
          text: "text-blue-700",
          icon: <FaCheckCircle className="h-5 w-5 text-blue-500" />,
        };
    }
  };

  const styles = getToastStyles();

  return (
    <motion.div
      initial={{ opacity: 0, y: -50, scale: 0.9 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: -50, scale: 0.9 }}
      transition={{ duration: 0.3, ease: "easeOut" }}
      className={`fixed top-4 right-4 z-50 max-w-sm w-full ${styles.bg} ${styles.border} rounded-lg shadow-lg border p-4`}
    >
      <div className="flex items-start gap-3">
        {styles.icon}
        <div className="flex-1">
          <p className={`font-medium text-sm ${styles.text}`}>
            {type === "success"
              ? "Success"
              : type === "error"
              ? "Error"
              : "Info"}
          </p>
          <p className={`text-sm ${styles.text} mt-1`}>{message}</p>
        </div>
        <button
          onClick={onClose}
          className={`${styles.text} hover:opacity-70 transition-opacity`}
        >
          <FaTimes className="h-4 w-4" />
        </button>
      </div>
    </motion.div>
  );
};

export default Toast;
