import React from 'react';

const Card = ({ children, className = '', title, subtitle }) => {
  return (
    <div className={`bg-white rounded-lg shadow-md p-6 ${className}`}>
      {(title || subtitle) && (
        <div className="mb-4">
          {title && <h2 className="text-xl font-bold text-gray-800">{title}</h2>}
          {subtitle && <p className="text-gray-600 mt-1">{subtitle}</p>}
        </div>
      )}
      {children}
    </div>
  );
};

export default Card;