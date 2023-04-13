using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SelectionStatements
{
    class Animal // This the base type for all animals
    {
        public string? Name;
        public DateTime Born;
        public byte Legs;
    }

    class Cat : Animal // This is a subtype of animal
    {
        public bool isDomestic;
    }

    class Spider : Animal // This is another subtype of animal
    {
        public bool isPoisonuos;
    }
}
