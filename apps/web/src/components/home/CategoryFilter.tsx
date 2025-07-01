
interface CategoryFilterProps {
  categories: Array<{
    id: string
    name: string
    active: boolean
  }>
  selectedCategory: string
  onCategorySelect: (categoryId: string) => void
}

export function CategoryFilter({ categories, selectedCategory, onCategorySelect }: CategoryFilterProps) {
  const displayCategories = categories

  return (
    <div className="px-6 mt-8">
      <div className="flex space-x-4 overflow-x-auto pb-2">
        {displayCategories.map((category) => {
          const isSelected = selectedCategory === category.id
          
          return (
            <button
              key={category.id}
              onClick={() => onCategorySelect(category.id)}
              className={`flex-shrink-0 px-4 py-2 rounded-full transition-all duration-200 ${
                isSelected
                  ? 'bg-transparent'
                  : 'bg-transparent'
              }`}
            >
              <span
                className={`text-base font-medium whitespace-nowrap ${
                  isSelected
                    ? 'text-[#FE9870] font-medium'
                    : 'text-[#D1D2D7] opacity-70'
                }`}
              >
                {category.name}
              </span>
              {isSelected && (
                <div className="w-full h-0.5 bg-[#FE9870] mt-1.5 rounded-full"></div>
              )}
            </button>
          )
        })}
      </div>
    </div>
  )
}