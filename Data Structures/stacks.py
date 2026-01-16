from typing import Any
from doubly_linkedlist import Node, DoublyLinkedList


class ArrayStack:
    def __init__(self):
        """
        파이썬 리스트(list)를 내부 저장소로 사용하는 스택을 초기화한다.

        - 스택의 top은 self.data의 마지막 원소(self.data[-1])에 해당한다.
        """
        self.data = []

    def size(self) -> int:
        """
        스택에 들어있는 원소의 개수를 반환한다.

        Returns:
            int: 스택 원소 개수
        """
        return len(self.data)

    def isEmpty(self) -> bool:
        """
        스택이 비어있는지 여부를 반환한다.

        Returns:
            bool: 비어있으면 True, 아니면 False
        """
        return self.size() == 0

    def push(self, item: Any) -> None:
        """
        스택 top에 item을 추가한다.

        Args:
            item (Any): 스택에 넣을 데이터

        Returns:
            None
        """
        self.data.append(item)

    def pop(self) -> Any:
        """
        스택 top의 원소를 제거하고 반환한다.

        Returns:
            Any: 제거된 top 원소

        Raises:
            IndexError: 스택이 비어있으면 발생 (list.pop()의 동작)
        """
        return self.data.pop()

    def peek(self) -> Any:
        """
        스택 top의 원소를 제거하지 않고 반환한다.

        Returns:
            Any: top 원소

        Raises:
            IndexError: 스택이 비어있으면 발생 (self.data[-1] 접근)
        """
        return self.data[-1]


class LinkedListStack:
    def __init__(self):
        """
        양방향 연결 리스트(DoublyLinkedList)를 내부 저장소로 사용하는 스택을 초기화한다.

        - 스택의 top은 연결 리스트의 '마지막 데이터 노드'에 해당한다.
        - push는 맨 뒤에 삽입, pop은 맨 뒤 삭제로 구현한다.
        """
        self.data = DoublyLinkedList()

    def size(self) -> int:
        """
        스택에 들어있는 원소의 개수를 반환한다.

        내부적으로는 연결 리스트의 길이(nodeCount)를 반환한다.

        Returns:
            int: 스택 원소 개수
        """
        return self.data.getLength()

    def isEmpty(self) -> bool:
        """
        스택이 비어있는지 여부를 반환한다.

        Returns:
            bool: 비어있으면 True, 아니면 False
        """
        return self.size() == 0

    def push(self, item: Any) -> None:
        """
        스택 top에 item을 추가한다.

        양방향 연결 리스트의 마지막 위치(nodeCount + 1)에 삽입한다.

        Args:
            item (Any): 스택에 넣을 데이터

        Returns:
            None
        """
        node = Node(item)
        self.data.insertAt(self.size() + 1, node)

    def pop(self) -> Any:
        """
        스택 top의 원소를 제거하고 반환한다.

        양방향 연결 리스트의 마지막 위치(nodeCount)를 삭제한다.

        Returns:
            Any: 제거된 top 원소

        Raises:
            IndexError: 스택이 비어있으면 발생 (popAt이 예외 발생)
        """
        return self.data.popAt(self.size())

    def peek(self) -> Any:
        """
        스택 top의 원소를 제거하지 않고 반환한다.

        Returns:
            Any: top 원소

        Raises:
            IndexError: 스택이 비어있으면 발생 (빈 스택에서 top 조회 불가)
        """
        if self.isEmpty():
            raise IndexError("peek from empty stack")

        node = self.data.getAt(self.size())
        assert node is not None
        
        return node.data
