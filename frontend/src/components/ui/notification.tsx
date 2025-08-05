import React, { useEffect } from "react";
import { cn } from "../../utils/cn";

interface NotificationProps {
  type: "success" | "error" | "warning" | "info";
  title: string;
  message: string;
  isVisible: boolean;
  onClose: () => void;
  autoClose?: boolean;
  autoCloseDelay?: number;
}

const Notification: React.FC<NotificationProps> = ({
  type,
  title,
  message,
  isVisible,
  onClose,
  autoClose = true,
  autoCloseDelay = 5000,
}) => {
  useEffect(() => {
    if (isVisible && autoClose) {
      const timer = setTimeout(() => {
        onClose();
      }, autoCloseDelay);

      return () => clearTimeout(timer);
    }
  }, [isVisible, autoClose, autoCloseDelay, onClose]);

  if (!isVisible) return null;

  const getTypeStyles = () => {
    switch (type) {
      case "success":
        return "bg-green-50 border-green-200 text-green-800";
      case "error":
        return "bg-red-50 border-red-200 text-red-800";
      case "warning":
        return "bg-yellow-50 border-yellow-200 text-yellow-800";
      case "info":
        return "bg-blue-50 border-blue-200 text-blue-800";
      default:
        return "bg-gray-50 border-gray-200 text-gray-800";
    }
  };

  return (
    <div className="fixed top-4 right-4 z-50 max-w-sm w-full">
      <div
        className={cn(
          "p-4 rounded-lg border shadow-lg transition-all duration-300",
          getTypeStyles()
        )}
      >
        <div className="flex justify-between items-start">
          <div className="flex-1">
            <h4 className="font-semibold text-sm mb-1">{title}</h4>
            <p className="text-sm opacity-90">{message}</p>
          </div>
          <button
            onClick={onClose}
            className="ml-4 text-current opacity-60 hover:opacity-100 transition-opacity"
          >
            <svg
              className="w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
};

export default Notification;
